<?php
/**
 * Theme supports and menus.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * Register theme supports and nav menu locations.
 */
function m11_setup() {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'custom-logo' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );

	register_nav_menus(
		array(
			'primary' => __( 'Primary', 'module11' ),
			'footer'  => __( 'Footer', 'module11' ),
		)
	);
}
add_action( 'after_setup_theme', 'm11_setup' );
