# -*- coding: utf-8 -*-
"""
Minimal stand-in for the (not-present-in-this-repo) figma-html-builder
`compile_html_blueprint.py`. Reads pages/<slug>/blueprint.json and writes a
static HTML package to pages/<slug>/dist/. Hand-written because no recipe
library / compiler tool exists on this machine - see docs/issues-log.md #17
and the mizuho-home planning session notes for why this had to be authored
directly instead of invoked as an external tool.
"""
import json
import html as htmllib
import os
import re
import sys

PAGE = 'mizuho-home'
ROOT = r'C:\Users\Vansh Patel\Local Sites\task-11\app\public'
PAGE_DIR = os.path.join(ROOT, 'pages', PAGE)
DIST_DIR = os.path.join(PAGE_DIR, 'dist')
ASSETS_DIR = os.path.join(DIST_DIR, 'assets')

with open(os.path.join(PAGE_DIR, 'blueprint.json'), encoding='utf-8') as f:
    BP = json.load(f)

os.makedirs(ASSETS_DIR, exist_ok=True)

SECTIONS = {s['id']: s for s in BP['sections']}


def esc(s):
    if s is None:
        return ''
    return htmllib.escape(str(s), quote=False)


def style_attr(overrides):
    if not overrides:
        return ''
    parts = '; '.join(f'{k}: {v}' for k, v in overrides.items())
    return f' style="{esc(parts)}"'


def responsive_css(section_id, overrides):
    if not overrides:
        return ''
    out = []
    for bp, vars_ in overrides.items():
        decls = '; '.join(f'{k}: {v}' for k, v in vars_.items())
        out.append(f'@media (max-width: {bp}px) {{ #{section_id} {{ {decls}; }} }}')
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Escape-hatch sections already carry their own literal html/css/js templates
# in blueprint.json. Resolve their {{ }} / {{#each}} / {{#unless}} placeholders
# by hand (small, section-specific renderers - no generic template engine
# available in this environment).
# ---------------------------------------------------------------------------

def render_hero_carousel(section):
    c = section['content_source']
    slides_html = []
    for i, slide in enumerate(c['slides']):
        lazy = '' if i == 0 else 'loading="lazy"'
        slides_html.append(f'''
        <div class="swiper-slide hero-carousel__slide">
          <a class="hero-carousel__card" href="{esc(slide['link'])}">
            <img class="hero-carousel__card-image" src="{esc(slide['image'])}" alt="{esc(slide['alt'])}" width="572" height="592" {lazy}>
            <span class="hero-carousel__label">{esc(slide['label'])}</span>
            <span class="hero-carousel__arrow" aria-hidden="true"><img src="figma/images/icon-arrow-circle-right.svg" alt="" width="55" height="55"></span>
          </a>
        </div>''')
    html_out = f'''
<section class="hero-carousel" id="hero-carousel">
  <div class="hero-carousel__inner">
    <h1 class="hero-carousel__heading">{esc(c['heading_main'])} <span class="hero-carousel__heading-accent">{esc(c['heading_accent'])}</span></h1>
    <div class="hero-carousel__swiper swiper">
      <div class="swiper-wrapper">{''.join(slides_html)}
      </div>
    </div>
    <div class="hero-carousel__actions-row">
      <a class="hero-carousel__cta hero-carousel__cta--primary" href="{esc(c['cta_primary']['url'])}">{esc(c['cta_primary']['label'])}</a>
      <a class="hero-carousel__cta hero-carousel__cta--secondary" href="{esc(c['cta_secondary']['url'])}">{esc(c['cta_secondary']['label'])}</a>
      <a class="hero-carousel__browse-link" href="{esc(c['browse_link']['url'])}"><img src="figma/images/icon-arrow-down.svg" alt="" width="14" height="14">{esc(c['browse_link']['label'])}</a>
      <div class="hero-carousel__pagination swiper-pagination"></div>
    </div>
  </div>
</section>'''
    return html_out, section['css'], section['js']


def render_procedure_band(section):
    c = section['content_source']
    items = []
    for p in c['procedures']:
        items.append(f'''
      <div class="procedure-band__item">
        <img class="procedure-band__icon" src="{esc(p['icon'])}" alt="" loading="lazy">
        <div class="procedure-band__text">
          <h3 class="procedure-band__title">{esc(p['title'])}</h3>
          <a class="procedure-band__link procedure-band__link--primary" href="{esc(p['link_primary']['url'])}">{esc(p['link_primary']['label'])} →</a>
          <a class="procedure-band__link procedure-band__link--secondary" href="{esc(p['link_secondary']['url'])}">{esc(p['link_secondary']['label'])} →</a>
        </div>
      </div>''')
    html_out = f'''
<section class="procedure-band" id="procedure-band">
  <div class="procedure-band__inner">
    <h2 class="procedure-band__heading">{esc(c['heading'])}</h2>
    <div class="procedure-band__grid">{''.join(items)}
    </div>
    <div class="procedure-band__closing">
      <p class="procedure-band__closing-text">{esc(c['closing_text'])}</p>
      <a class="procedure-band__button" href="{esc(c['button']['url'])}">{esc(c['button']['label'])} <img src="figma/images/icon-arrow-down.svg" alt="" width="14" height="14"></a>
    </div>
  </div>
</section>'''
    return html_out, section['css'], section.get('js', '')


def render_about_stats(section):
    c = section['content_source']
    stats = []
    for s in c['stats']:
        stats.append(f'''
      <div class="about-stats__stat about-stats__stat--{esc(s['variant'])}">
        <div class="about-stats__panel"></div>
        <div class="about-stats__card">
          <span class="about-stats__number">{esc(s['number'])}</span>
          <span class="about-stats__label">{esc(s['label'])}</span>
        </div>
      </div>''')
    html_out = f'''
<section class="about-stats" id="about-stats">
  <div class="about-stats__inner">
    <h2 class="about-stats__heading">{esc(c['heading'])}</h2>
    <p class="about-stats__body">{esc(c['body'])}</p>
    <div class="about-stats__row">{''.join(stats)}
    </div>
    <a class="about-stats__button" href="{esc(c['button']['url'])}">{esc(c['button']['label'])}</a>
  </div>
</section>'''
    return html_out, section['css'], section.get('js', '')


# ---------------------------------------------------------------------------
# Recipe sections: no recipe library ships with this repo, so the recipe
# markup itself is authored here (matching the BEM class names already used
# by blueprint.json's style_overrides / extra_css for these three recipes).
# ---------------------------------------------------------------------------

def render_hero_centered(section):
    c = section['content_source']
    style = style_attr(section.get('style_overrides'))
    html_out = f'''
<section class="hero-centered hero-centered--intro-statement" id="intro-statement"{style}>
  <div class="hero-centered__inner">
    <h2 class="hero-centered__title">{esc(c['heading'])}</h2>
    <p class="hero-centered__desc">{esc(c['body'])}</p>
    <a class="hero-centered__cta" href="{esc(c['cta']['url'])}">{esc(c['cta']['label'])}</a>
  </div>
</section>'''
    base_css = '''
.hero-centered { padding: 60px 40px; text-align: center; background: var(--clr-white); }
.hero-centered__inner { max-width: var(--hero-content-width, 900px); margin: 0 auto; }
.hero-centered__title { font-family: 'Freeman', sans-serif; font-size: var(--hero-title-size, 2.5rem); line-height: var(--hero-title-line-height, 1.2); margin: 0 0 20px; }
.hero-centered__desc { font-size: var(--hero-desc-size, 1.125rem); margin: 0 0 24px; }
.hero-centered__cta { display: inline-block; text-decoration: none; }
'''
    return html_out, base_css, section.get('extra_css', ''), responsive_css('intro-statement', section.get('responsive_style_overrides'))


def render_card_grid_3col(section):
    c = section['content_source']
    style = style_attr(section.get('style_overrides'))
    cards = []
    for card in c['cards']:
        cards.append(f'''
      <div class="card-grid-3col__card">
        <img class="card-grid-3col__icon" src="{esc(card['icon'])}" alt="" loading="lazy">
        <h3 class="card-grid-3col__title">{esc(card['title'])}</h3>
        <p class="card-grid-3col__lead">{esc(card['lead'])}</p>
        <p class="card-grid-3col__body">{esc(card['body'])}</p>
      </div>''')
    html_out = f'''
<section class="card-grid-3col card-grid-3col--value-columns" id="value-columns"{style}>
  <div class="card-grid-3col__grid">{''.join(cards)}
  </div>
  <a class="card-grid-3col__button" href="{esc(c['button']['url'])}">{esc(c['button']['label'])}</a>
</section>'''
    base_css = '''
.card-grid-3col { background: var(--clr-white); }
.card-grid-3col__grid { display: grid; grid-template-columns: repeat(var(--grid-cols, 3), 1fr); gap: var(--grid-gap, 24px); }
.card-grid-3col__title { font-size: var(--card-title-size, 1.25rem); margin: 0 0 12px; }
@media (max-width: 768px) { .card-grid-3col__grid { grid-template-columns: repeat(var(--grid-cols-tablet, 2), 1fr); } }
@media (max-width: 430px) { .card-grid-3col__grid { grid-template-columns: repeat(var(--grid-cols-mobile, 1), 1fr); } }
'''
    return html_out, base_css, section.get('extra_css', ''), responsive_css('value-columns', section.get('responsive_style_overrides'))


def render_testimonial_grid(section):
    c = section['content_source']
    style = style_attr(section.get('style_overrides'))
    cards = []
    for card in c['cards']:
        cards.append(f'''
      <div class="testimonial-grid__card">
        <div class="testimonial-grid__thumb-wrap">
          <img class="testimonial-grid__thumb" src="{esc(card['thumbnail'])}" alt="{esc(card['alt'])}" loading="lazy">
          <img class="testimonial-grid__play-icon" src="figma/images/icon-play-circle.svg" alt="">
        </div>
        <p class="testimonial-grid__name">{esc(card['name'])}</p>
        <p class="testimonial-grid__role">{card['role_html']}</p>
        <a class="testimonial-grid__cta" href="{esc(card['video_url'])}">{esc(card['cta_label'])}</a>
      </div>''')
    html_out = f'''
<section class="testimonial-grid testimonial-grid--testimonials" id="testimonials"{style}>
  <h2 class="testimonial-grid__eyebrow">{esc(c['eyebrow'])}</h2>
  <p class="testimonial-grid__intro">{c['intro']}</p>
  <div class="testimonial-grid__grid">{''.join(cards)}
  </div>
  <div class="testimonial-grid__featured-quote">
    <blockquote>{esc(c['featured_quote']['quote'])}</blockquote>
    <cite>{esc(c['featured_quote']['attribution'])}</cite>
    <div class="testimonial-grid__more-cta-row"><a class="testimonial-grid__more-cta" href="{esc(c['more_cta']['url'])}">{esc(c['more_cta']['label'])}</a></div>
  </div>
  <a class="testimonial-grid__mobile-extra-cta" href="#intro-statement">Watch what clinical experts say about us</a>
</section>'''
    base_css = '''
.testimonial-grid { background: var(--clr-white); }
.testimonial-grid__grid { display: grid; grid-template-columns: repeat(var(--grid-cols, 3), 1fr); gap: var(--grid-gap, 24px); }
.testimonial-grid__thumb-wrap { position: relative; }
.testimonial-grid__mobile-extra-cta { display: none; }
@media (max-width: 430px) {
  .testimonial-grid__grid { grid-template-columns: repeat(var(--grid-cols-mobile, 1), 1fr); }
  .testimonial-grid__mobile-extra-cta { display: block; text-align: center; text-decoration: none; }
}
'''
    return html_out, base_css, section.get('extra_css', ''), responsive_css('testimonials', section.get('responsive_style_overrides'))


def render_header_placeholder(section):
    c = section['content_source']
    nav = ''.join(f'<a href="#">{esc(i)}</a>' for i in c['nav_items'])
    return f'''
<header class="site-header-placeholder" id="site-header-placeholder">
  <!-- OUT OF SCOPE: placeholder only, for visual context. Real header = Elementor Theme Builder template 61. -->
  <img class="site-header-placeholder__logo" src="{esc(c['logo'])}" alt="Mizuho America" height="40">
  <nav class="site-header-placeholder__nav">{nav}</nav>
  <a class="site-header-placeholder__cta" href="#">{esc(c['cta_label'])}</a>
</header>'''


def render_footer_placeholder(section):
    c = section['content_source']
    cols = ''.join(
        f'<div><h4>{esc(col["heading"])}</h4><a href="#">Link</a></div>' for col in c['columns']
    )
    return f'''
<footer class="site-footer-placeholder" id="site-footer-placeholder">
  <!-- OUT OF SCOPE: placeholder only, for visual context. Real footer = Elementor Theme Builder template 62 + ACF Site Settings. -->
  <div class="site-footer-placeholder__cols">{cols}</div>
  <img class="site-footer-placeholder__logo" src="{esc(c['logo'])}" alt="Mizuho America" height="36">
  <p>{esc(c['copyright'])}</p>
</footer>'''


BASE_CSS = '''
:root {
  --clr-primary: #0065B3;
  --clr-sky: #00B3F0;
  --clr-navy: #002842;
  --clr-text: #090909;
  --clr-white: #FFFFFF;
  --clr-light-sky: #77DCFF;
  --clr-dot: #D9D9D9;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Open Sans', sans-serif; color: var(--clr-text); }
img { max-width: 100%; display: block; }
a { color: inherit; text-decoration: none; }
.site-container { max-width: 1240px; margin: 0 auto; padding: 0 20px; }
.site-header-placeholder, .site-footer-placeholder { background: #eef6fb; padding: 16px 24px; display: flex; align-items: center; gap: 24px; font-family: 'Open Sans', sans-serif; font-size: 13px; }
.site-footer-placeholder { background: var(--clr-primary); color: #fff; flex-direction: column; align-items: flex-start; }
.site-footer-placeholder__cols { display: flex; gap: 40px; }
.site-header-placeholder__nav { display: flex; gap: 16px; margin-left: auto; }
'''

order = [
    'site-header-placeholder',
    'hero-carousel',
    'intro-statement',
    'value-columns',
    'procedure-band',
    'testimonials',
    'about-stats',
    'site-footer-placeholder',
]

body_html_parts = []
css_parts = [BASE_CSS]
js_parts = []

for sid in order:
    section = SECTIONS[sid]
    if sid == 'hero-carousel':
        h, css, js = render_hero_carousel(section)
        body_html_parts.append(h)
        css_parts.append(css)
        js_parts.append(js)
    elif sid == 'intro-statement':
        h, base_css, extra_css, resp = render_hero_centered(section)
        body_html_parts.append(h)
        css_parts.extend([base_css, extra_css, resp])
    elif sid == 'value-columns':
        h, base_css, extra_css, resp = render_card_grid_3col(section)
        body_html_parts.append(h)
        css_parts.extend([base_css, extra_css, resp])
    elif sid == 'procedure-band':
        h, css, js = render_procedure_band(section)
        body_html_parts.append(h)
        css_parts.append(css)
        if js:
            js_parts.append(js)
    elif sid == 'testimonials':
        h, base_css, extra_css, resp = render_testimonial_grid(section)
        body_html_parts.append(h)
        css_parts.extend([base_css, extra_css, resp])
    elif sid == 'about-stats':
        h, css, js = render_about_stats(section)
        body_html_parts.append(h)
        css_parts.append(css)
        if js:
            js_parts.append(js)
    elif sid == 'site-header-placeholder':
        body_html_parts.append(render_header_placeholder(section))
        if section.get('extra_css'):
            css_parts.append(section['extra_css'])
    elif sid == 'site-footer-placeholder':
        body_html_parts.append(render_footer_placeholder(section))

fonts_param = 'Freeman|Open+Sans:wght@300;400;600;700|Montserrat:wght@300;500;700|Mukta:wght@700|Fraunces:wght@700'
google_fonts_link = f'https://fonts.googleapis.com/css2?family={fonts_param}&display=swap'

html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(BP['meta']['title'])}</title>
<meta name="description" content="{esc(BP['meta']['description'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{google_fonts_link}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
{''.join(body_html_parts)}
<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
<script src="assets/main.js"></script>
</body>
</html>
'''

with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_doc)

with open(os.path.join(ASSETS_DIR, 'style.css'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(css_parts))

with open(os.path.join(ASSETS_DIR, 'main.js'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(js_parts))

print('Compiled:')
print(' -', os.path.join(DIST_DIR, 'index.html'))
print(' -', os.path.join(ASSETS_DIR, 'style.css'))
print(' -', os.path.join(ASSETS_DIR, 'main.js'))
