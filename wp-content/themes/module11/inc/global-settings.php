<?php
/**
 * Global settings bridge (Flow B).
 *
 * Brand colours and fonts are stored once (ACF Site Settings) and printed as CSS custom
 * properties, so every SCSS partial reads var(--clr-*) and never a hardcoded hex.
 * The field names are added when the global settings field group is built.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * Get a Site Settings value with a fallback when ACF is inactive or the field is empty.
 *
 * @param string $name     Field name on the options page.
 * @param mixed  $fallback Value returned when empty.
 * @return mixed
 */
function m11_get_setting( $name, $fallback = '' ) {
	if ( ! function_exists( 'get_field' ) ) {
		return $fallback;
	}

	$value = get_field( $name, 'options' );

	return ( '' === $value || null === $value || false === $value ) ? $fallback : $value;
}

/**
 * Print brand tokens from Site Settings as CSS custom properties.
 */
function m11_print_brand_tokens() {
	$map = apply_filters( 'm11_brand_token_map', array() ); // 'css-var-name' => 'acf_field_name'.
	$css = '';

	foreach ( $map as $var => $field ) {
		$value = sanitize_hex_color( (string) m11_get_setting( $field ) );
		if ( $value ) {
			$css .= '--' . sanitize_key( $var ) . ':' . $value . ';';
		}
	}

	if ( $css ) {
		printf( "<style id=\"m11-brand-tokens\">:root{%s}</style>\n", esc_html( $css ) );
	}
}
add_action( 'wp_head', 'm11_print_brand_tokens', 5 );
