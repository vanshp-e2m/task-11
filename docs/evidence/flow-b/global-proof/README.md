# Global settings proof (Flow B)

One edit each, then revert: **Site Settings → Phone** `800-699-2547` → `800-555-0199`, and **Elementor Kit → Primary** `#0065b3` → `#b0197e`. No page, template or widget was edited.

| Page | Builder | Phone shown before → after (old number left) | tel: links before → after | First heading colour before → after → reverted |
|---|---|---|---|---|
| Home | ACF | 2 → 2 (0) | 2 → 2 | `rgb(0, 101, 179)` → `rgb(176, 25, 126)` → `rgb(0, 101, 179)` |
| Resources | ACF | 2 → 2 (0) | 2 → 2 | `rgb(0, 101, 179)` → `rgb(176, 25, 126)` → `rgb(0, 101, 179)` |
| Products | ACF | 2 → 2 (0) | 2 → 2 | `rgb(0, 101, 179)` → `rgb(176, 25, 126)` → `rgb(0, 101, 179)` |
| Product (CPT) | ACF | 2 → 2 (0) | 2 → 2 | `rgb(0, 101, 179)` → `rgb(176, 25, 126)` → `rgb(0, 101, 179)` |
| About Us | Elementor | 2 → 2 (0) | 2 → 2 | `rgb(0, 101, 179)` → `rgb(176, 25, 126)` → `rgb(0, 101, 179)` |
| Contact Us | Elementor | 3 → 3 (0) | 3 → 3 | `rgb(0, 101, 179)` → `rgb(176, 25, 126)` → `rgb(0, 101, 179)` |
| Sales Hub login | ACF | 0 → 0 (0) | 0 → 0 | `rgb(0, 101, 179)` → `rgb(176, 25, 126)` → `rgb(0, 101, 179)` |

Screenshots (1440, top of page): `1-before-*.png`, `2-after-*.png`, `3-reverted-*.png` for Home (ACF), Contact Us and About Us (Elementor): the header phone, the Contact card, the footer and the headings change together.

**How it's wired:** the phone lives in ACF Site Settings; Elementor reads it through the theme's dynamic tags (`inc/elementor/class-m11-tag-setting-*.php`, header, footer, Contact card), ACF templates through `m11_get_setting()`. The colour lives in the Elementor Kit; Elementor widgets use `__globals__`, the ACF partials use `var(--clr-primary)`, which `abstracts/_tokens.scss` maps to `--e-global-color-primary` (the generated partials were tokenised for this: issues-log #66).

## Writes (DevConnect via tools/bridge.py, read back)

- m11_phone := 800-555-0199 (read back 800-555-0199); Kit primary := #b0197e (read back #b0197e, other slots unchanged: ['#00b3f0', '#090909', '#002842'] + 3 custom)
- m11_phone := 800-699-2547 (read back 800-699-2547); Kit primary := #0065b3 (read back #0065b3, other slots unchanged: ['#00b3f0', '#090909', '#002842'] + 3 custom)
