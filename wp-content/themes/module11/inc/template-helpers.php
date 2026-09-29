<?php
/**
 * Template helpers: the Flexible Content dispatcher plus the shared render helpers
 * every section partial uses (section attrs, accent kses, multiline, image, button,
 * section head, text link, line-block renderers).
 *
 * Contract (HTML -> ACF pipeline, step 4):
 * - Partials are transplanted from the verbatim spec fragments; these helpers only
 *   emit markup whose SHAPE matches the fragment node they replace.
 * - Every helper returns an already-escaped string (esc_attr / esc_html / esc_url /
 *   wp_kses inside) so partials can `echo` the return value directly.
 * - Clone fields are `display: seamless`, so common_settings sub-fields are read by
 *   their own names with get_sub_field() inside the FC row.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/* -------------------------------------------------------------------------
 * Flexible Content dispatch
 * ---------------------------------------------------------------------- */

/**
 * Render every Flexible Content row for the current post.
 *
 * Layout name (snake_case) maps to template-parts/flex-blocks/{kebab-case}.php
 * (house convention: one layout = one template part).
 *
 * @param string $field Flexible Content field name.
 */
function m11_render_sections( $field = 'sections' ) {
	if ( ! function_exists( 'have_rows' ) || ! have_rows( $field ) ) {
		return;
	}

	$page_scope = get_post_field( 'post_name', get_queried_object_id() );

	while ( have_rows( $field ) ) {
		the_row();
		$layout = sanitize_key( get_row_layout() );
		if ( ! $layout ) {
			continue;
		}
		// Layout styles are scoped to the page they were converted from (the replicas reuse class names). When a layout is used
		// on any other page (a new page, a renamed slug), wrap it in that origin scope so it keeps its design (issues-log #63).
		$origin = m11_layout_scope( $layout );
		$wrap   = $origin && $origin !== $page_scope;
		if ( $wrap ) {
			echo '<div class="m11-layout-scope m11-page-' . esc_attr( $origin ) . '">';
		}
		get_template_part( 'template-parts/flex-blocks/' . str_replace( '_', '-', $layout ) );
		if ( $wrap ) {
			echo '</div>';
		}
	}
}

/**
 * The page scope a layout's SCSS partial is written against (tools/figma_html/split_replica_css.py PAGES).
 *
 * @param string $layout Layout name (snake_case).
 * @return string Scope slug, or '' for an unknown layout.
 */
function m11_layout_scope( $layout ) {
	$scopes = array(
		'mizuho-home'      => array( 'hero_carousel', 'intro_statement', 'value_columns', 'procedure_band', 'testimonial_home', 'about_stats' ),
		'resources'        => array( 'resources_intro', 'resources_testimonials', 'fast_facts', 'resources_brochures', 'bottom_links_band' ),
		'products'         => array( 'products_intro', 'browse_by_procedure', 'browse_by_product' ),
		'sales-hub'        => array( 'sh_login' ),
		'dashboard'        => array( 'sh_dashboard', 'sh_account' ),
		'resource-library' => array( 'sh_resource_library_intro', 'sh_resource_results' ),
	);
	foreach ( $scopes as $scope => $layouts ) {
		if ( in_array( $layout, $layouts, true ) ) {
			return $scope;
		}
	}
	return '';
}

/* -------------------------------------------------------------------------
 * common_settings (seamless clone) contract
 * ---------------------------------------------------------------------- */

/**
 * True when the editor ticked common_settings > hide_section for the current row.
 *
 * @return bool
 */
function m11_section_is_hidden() {
	$hide = get_sub_field( 'hide_section' );

	if ( is_array( $hide ) ) {
		return in_array( 'hidden', $hide, true );
	}

	return 'hidden' === $hide;
}

/**
 * Sanitised common_settings > sec_id for the current row ('' when unset).
 * Doubles as the in-page anchor target (never falls back to a hardcoded id).
 *
 * @return string
 */
function m11_section_id() {
	$id = (string) get_sub_field( 'sec_id' );
	$id = preg_replace( '/[^A-Za-z0-9_-]/', '', ltrim( trim( $id ), '#' ) );

	return (string) $id;
}

/**
 * Attribute string for a section's root element, in the fragment's attribute order:
 * class (the fragment's own root classes), id (common_settings > sec_id, only when set),
 * data-section-id (static spec id).
 *
 * common_settings is deliberately limited to hide_section + sec_id: brand colours and
 * spacing are central (Elementor Kit / theme tokens), not per-section pickers.
 *
 * Usage: <section<?php echo m11_section_attrs( 'hero rs', 'hero-carousel' ); ?>>
 *
 * @param string $classes   The fragment's own root classes, verbatim.
 * @param string $source_id The spec section id (static hook for QA / JS).
 * @return string Escaped attribute string with a leading space.
 */
function m11_section_attrs( $classes, $source_id = '' ) {
	$class_list = array_filter( array_map( 'sanitize_html_class', preg_split( '/\s+/', trim( $classes ) ) ) );

	$out = ' class="' . esc_attr( implode( ' ', $class_list ) ) . '"';

	$id = m11_section_id();
	if ( $id ) {
		$out .= ' id="' . esc_attr( $id ) . '"';
	}

	if ( $source_id ) {
		$out .= ' data-section-id="' . esc_attr( $source_id ) . '"';
	}

	return $out;
}

/**
 * href for a label whose link lives in a sibling `*_url` field: the editor's value when
 * set, otherwise the template default (the fragment's own in-page anchor).
 *
 * @param mixed  $value    The `*_url` field value (url string or ACF link array).
 * @param string $fallback Default href.
 * @return string Unescaped URL.
 */
function m11_href( $value, $fallback = '#' ) {
	$url = is_array( $value ) ? ( isset( $value['url'] ) ? (string) $value['url'] : '' ) : trim( (string) $value );

	return '' !== $url ? $url : $fallback;
}

/**
 * '#sec_id' for the current row, or '' when no sec_id is set (used for self-targeting
 * form actions / pager links that the fragment pointed at the section's own id).
 *
 * @return string
 */
function m11_section_hash() {
	$id = m11_section_id();

	return $id ? '#' . $id : '';
}

/* -------------------------------------------------------------------------
 * Text helpers
 * ---------------------------------------------------------------------- */

/**
 * Restricted kses for accent headlines / short labels: em, span, strong, br (+ class).
 *
 * @param string $text Raw field value.
 * @return string
 */
function m11_accent_kses( $text ) {
	$allowed = array(
		'em'     => array( 'class' => true ),
		'span'   => array( 'class' => true ),
		'strong' => array( 'class' => true ),
		'br'     => array( 'class' => true ),
	);

	return wp_kses( (string) $text, $allowed );
}

/**
 * Split a textarea value into trimmed, non-empty lines.
 *
 * @param string $text Raw textarea value (new_lines: '').
 * @return string[]
 */
function m11_lines( $text ) {
	$lines = preg_split( '/\r\n|\r|\n/', (string) $text );

	return array_values( array_filter( array_map( 'trim', $lines ), 'strlen' ) );
}

/**
 * Multiline textarea -> escaped text joined by <br> (the fragment's own <br> shape,
 * optionally with a class such as "d-only" for desktop-only breaks).
 *
 * @param string $text     Raw textarea value.
 * @param string $br_class Optional class for the <br> tags.
 * @return string
 */
function m11_multiline( $text, $br_class = '' ) {
	$lines = preg_split( '/\r\n|\r|\n/', trim( (string) $text ) );
	$br    = $br_class ? '<br class="' . esc_attr( $br_class ) . '">' : '<br>';

	return implode( $br, array_map( 'esc_html', $lines ) );
}

/**
 * Render a text value as the fragment's <span>/<strong> run (e.g. `.pd-model`,
 * `.pd-facts`, `.pd-part`): editors mark the bold part with <strong>…</strong>;
 * every run gets the size utility class.
 *
 * "Part no.: <strong>FB-0480</strong> • Available in 6 sizes" (class s14) ->
 * <span class="s14">Part no.: </span><strong class="s14">FB-0480</strong><span class="s14"> • Available in 6 sizes</span>
 *
 * @param string $text  Raw text (may contain <strong>).
 * @param string $class Size utility class for every run.
 * @return string
 */
function m11_strong_runs( $text, $class ) {
	$parts = preg_split( '#(<strong[^>]*>.*?</strong>)#i', (string) $text, -1, PREG_SPLIT_DELIM_CAPTURE | PREG_SPLIT_NO_EMPTY );
	$out   = '';

	foreach ( $parts as $part ) {
		if ( preg_match( '#^<strong[^>]*>(.*?)</strong>$#is', $part, $m ) ) {
			$out .= '<strong class="' . esc_attr( $class ) . '">' . esc_html( wp_strip_all_tags( $m[1] ) ) . '</strong>';
		} else {
			$out .= '<span class="' . esc_attr( $class ) . '">' . esc_html( wp_strip_all_tags( $part ) ) . '</span>';
		}
	}

	return $out;
}

/**
 * Render a textarea as the fragment's "line block" (<p class="ln …"> per line), used by
 * `.tx-bio` (Resources testimonials) and `.bg-copy` (Resources brochures).
 *
 * @param string $text  Raw textarea value.
 * @param array  $rules List of [ p_class, inner_tag, inner_class ] by line index; the last
 *                      rule repeats for every further line.
 * @return string
 */
function m11_line_block( $text, $rules ) {
	$out = '';

	foreach ( m11_lines( $text ) as $i => $line ) {
		$rule  = isset( $rules[ $i ] ) ? $rules[ $i ] : end( $rules );
		$out  .= '<p class="' . esc_attr( $rule[0] ) . '"><' . tag_escape( $rule[1] ) . ' class="' . esc_attr( $rule[2] ) . '">'
			. esc_html( $line ) . '</' . tag_escape( $rule[1] ) . '></p>';
	}

	return $out;
}

/**
 * Section head: heading element whose tag comes from the heading_tag select
 * (title/content/CTA clone), falling back to the fragment's own tag.
 *
 * @param string $tag      heading_tag value.
 * @param string $text     Heading text (restricted kses).
 * @param string $class    Fragment class for the heading.
 * @param string $fallback Fragment's tag.
 * @return string
 */
function m11_section_head( $tag, $text, $class, $fallback = 'h2' ) {
	if ( '' === trim( (string) $text ) ) {
		return '';
	}

	$tag = in_array( $tag, array( 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span' ), true ) ? $tag : $fallback;

	return '<' . $tag . ' class="' . esc_attr( $class ) . '">' . m11_accent_kses( $text ) . '</' . $tag . '>';
}

/* -------------------------------------------------------------------------
 * Links / buttons
 * ---------------------------------------------------------------------- */

/**
 * Normalise an ACF link (return_format array) or a plain URL string.
 *
 * @param mixed $link ACF link array or URL.
 * @return array { url, title, target }
 */
function m11_link( $link ) {
	if ( is_array( $link ) ) {
		return array(
			'url'    => isset( $link['url'] ) ? (string) $link['url'] : '',
			'title'  => isset( $link['title'] ) ? (string) $link['title'] : '',
			'target' => isset( $link['target'] ) ? (string) $link['target'] : '',
		);
	}

	return array(
		'url'    => (string) $link,
		'title'  => '',
		'target' => '',
	);
}

/**
 * href (+ target/rel when the editor chose "open in new tab") attribute string.
 *
 * @param mixed $link ACF link array or URL.
 * @return string Escaped attribute string with a leading space ('' when no URL).
 */
function m11_link_attrs( $link ) {
	$link = m11_link( $link );

	if ( '' === $link['url'] ) {
		return '';
	}

	$out = ' href="' . esc_url( $link['url'] ) . '"';
	if ( '_blank' === $link['target'] ) {
		$out .= ' target="_blank" rel="noopener"';
	}

	return $out;
}

/**
 * Button / text link: <a class="…" href="…">{before}{label}</a>.
 * Label = the explicit label field when set, otherwise the link's own title.
 * Returns '' when there is no URL or no label (optional fields render nothing).
 *
 * @param mixed  $link        ACF link array or URL.
 * @param string $label       Explicit label (may be '').
 * @param string $class       Fragment classes for the <a>.
 * @param string $before_html Trusted static inner markup before the label (e.g. the
 *                            fragment's decorative `<span class="dl-arrow" aria-hidden="true"></span>`).
 * @param bool   $accent      Render the label through the accent kses (allows <br>).
 * @return string
 */
function m11_button( $link, $label, $class, $before_html = '', $accent = false ) {
	$attrs = m11_link_attrs( $link );
	$label = '' !== trim( (string) $label ) ? (string) $label : m11_link( $link )['title'];

	if ( '' === $attrs || '' === trim( $label ) ) {
		return '';
	}

	$label_html = $accent ? m11_accent_kses( $label ) : esc_html( $label );

	return '<a class="' . esc_attr( $class ) . '"' . $attrs . '>' . $before_html . $label_html . '</a>';
}

/**
 * Text link: label field + href (resolved by the partial, usually via m11_href()).
 *
 * @param string $href        Fragment href (in-page anchor or site path).
 * @param string $label       Label field value.
 * @param string $class       Fragment classes.
 * @param string $inner_open  Trusted static markup before the label.
 * @param string $inner_close Trusted static markup after the label.
 * @return string
 */
function m11_text_link( $href, $label, $class, $inner_open = '', $inner_close = '' ) {
	if ( '' === trim( (string) $label ) ) {
		return '';
	}

	return '<a class="' . esc_attr( $class ) . '" href="' . esc_url( $href ) . '">' . $inner_open . esc_html( $label ) . $inner_close . '</a>';
}

/* -------------------------------------------------------------------------
 * Images
 * ---------------------------------------------------------------------- */

/**
 * Attachment image via wp_get_attachment_image() (house rule), lazy by default.
 * Pass 'loading' => false for the hero / above-the-fold image; pass 'alt' => '' for
 * decorative icons (the fragment's alt=""), otherwise the attachment's own alt is used.
 *
 * @param int    $id    Attachment ID.
 * @param array  $attrs Extra attributes (class, alt, loading, …).
 * @param string $size  Image size.
 * @return string
 */
function m11_image( $id, $attrs = array(), $size = 'full' ) {
	$id = (int) $id;

	if ( ! $id ) {
		return '';
	}

	$attrs = wp_parse_args( $attrs, array( 'loading' => 'lazy' ) );

	return (string) wp_get_attachment_image( $id, $size, false, $attrs );
}

/**
 * URL of a decorative theme icon (static, aria-hidden / alt="" in the fragment).
 * These are theme assets, not content: assets/images/icons/{file}.
 *
 * @param string $file Icon file name.
 * @return string Escaped URL.
 */
function m11_icon_url( $file ) {
	return esc_url( get_theme_file_uri( 'assets/images/icons/' . $file ) );
}

/* -------------------------------------------------------------------------
 * Site URLs used by structural (non-content) links
 * ---------------------------------------------------------------------- */

/**
 * Permalink of a page by path, filterable ('m11_page_url'), '' when the page is missing.
 *
 * @param string $path Page path, e.g. 'products' or 'sales-hub/dashboard'.
 * @return string
 */
function m11_page_url( $path ) {
	$m11_page = get_page_by_path( $path );
	$url      = $m11_page ? get_permalink( $m11_page ) : '';

	return (string) apply_filters( 'm11_page_url', $url, $path );
}
