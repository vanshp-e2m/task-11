<?php
/**
 * Elementor dynamic tags that read ACF Site Settings.
 *
 * Lets the Elementor header/footer/pages show the same phone, email, address, hours and logo the ACF
 * templates use, so one edit in Site Settings updates every page, whichever builder made it.
 * Elementor's own ACF tags can't build tel:/mailto: links or return an options-page logo reliably, hence these.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * Site Settings fields exposed to Elementor, grouped by what they return.
 *
 * @return array
 */
function m11_elementor_tag_fields() {
	return array(
		'text'  => array(
			'm11_phone'    => __( 'Phone', 'module11' ),
			'm11_fax'      => __( 'Fax', 'module11' ),
			'm11_email'    => __( 'Email', 'module11' ),
			'm11_hours'    => __( 'Opening hours', 'module11' ),
			'm11_address'  => __( 'Address', 'module11' ),
			'm11_hub_name' => __( 'Sales Hub name', 'module11' ),
		),
		'link'  => array(
			'm11_phone' => __( 'Phone (tap to call)', 'module11' ),
			'm11_fax'   => __( 'Fax (tel: link)', 'module11' ),
			'm11_email' => __( 'Email (mailto: link)', 'module11' ),
		),
		'image' => array(
			'm11_logo'          => __( 'Logo (header)', 'module11' ),
			'm11_logo_reversed' => __( 'Logo (footer, white)', 'module11' ),
		),
	);
}

/**
 * Build a tel: or mailto: URL from a Site Settings value.
 *
 * @param string $field Field name.
 * @return string
 */
function m11_setting_link_url( $field ) {
	$value = (string) m11_get_setting( $field );
	if ( '' === $value ) {
		return '';
	}

	if ( 'm11_email' === $field ) {
		return is_email( $value ) ? 'mailto:' . $value : '';
	}

	$digits = preg_replace( '/[^0-9+]/', '', $value );
	return $digits ? 'tel:' . $digits : '';
}

/**
 * Register the "Site Settings" tag group and its tags.
 *
 * @param \Elementor\Core\DynamicTags\Manager $dynamic_tags Tag manager.
 */
function m11_register_elementor_tags( $dynamic_tags ) {
	require_once M11_DIR . '/inc/elementor/class-m11-tag-setting-text.php';
	require_once M11_DIR . '/inc/elementor/class-m11-tag-setting-link.php';
	require_once M11_DIR . '/inc/elementor/class-m11-tag-setting-image.php';

	$dynamic_tags->register_group( 'm11-site-settings', array( 'title' => __( 'Site Settings', 'module11' ) ) );
	$dynamic_tags->register( new M11_Tag_Setting_Text() );
	$dynamic_tags->register( new M11_Tag_Setting_Link() );
	$dynamic_tags->register( new M11_Tag_Setting_Image() );
}
add_action( 'elementor/dynamic_tags/register', 'm11_register_elementor_tags' );
